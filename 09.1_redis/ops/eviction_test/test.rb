require 'redis'
require 'connection_pool'
require 'timeout'
require 'benchmark'

class Test
  attr_reader :redis_pool, :experiments_count, :threads_count, :keys_count, :ttl_max, :logging

  def initialize(host:, experiments_count:, threads_count:, keys_count:, ttl_max:, logging: false)
    @experiments_count = experiments_count
    @keys_count = keys_count
    @ttl_max = ttl_max
    @logging = logging
    @threads_count = threads_count
    @redis_pool = ConnectionPool.new(size: threads_count) { Redis.new(host: host) }
  end

  def call
    redis_pool.with { |redis| redis.flushall; redis.flushdb }

    threads_count.times.map do |i|
      Thread.new do
        experiments_count.times do
        # Timeout.timeout(TIMEOUT_IN_SECONDS) do
          n = rand(keys_count)
          get(n) || set(n)
        end
      end
    end
    .each(&:join)
  end

  private

  def get(n)
    redis_pool.with do |redis|
      redis.get(n.to_s).tap { |res| log('-') if res }
    end
  end

  def set(n, value_multiplier: 100)
    redis_pool.with do |redis|
      log('+')
      redis.set(n.to_s, n.to_s * value_multiplier, px: rand(ttl_max) + 1)
    end
  end

  def log(symbol)
    print(symbol) if logging
  end
end

class Metatest
  EXPERIMENTS_COUNT = 10_000
  KEYS_COUNT = 10_000
  TTL_MAX = 1_000_000
  LOGGING = false

  HOSTS = %w[
    redis-volatile-lru
    redis-volatile-lfu
    redis-volatile-random
    redis-volatile-ttl
    redis-allkeys-lru
    redis-allkeys-lfu
    redis-allkeys-random
  ].freeze

  def call
    Benchmark.bm do |benchmark|
      HOSTS.each do |host|
        benchmark.report((host + '     ')[..20]) do
          Test.new(host: host, **params).call
        end
      end
    end
  end

  private

  def threads_count
    @threads_count ||= begin
      result = ARGV[0]
      raise ArgumentError, 'Please, pass threads count as a parameter' unless result
      Integer(result)
    end
  end

  def params
    {
      experiments_count: EXPERIMENTS_COUNT,
      threads_count: threads_count,
      keys_count: KEYS_COUNT,
      ttl_max: TTL_MAX,
      logging: LOGGING
    }
  end
end

Metatest.new.call
