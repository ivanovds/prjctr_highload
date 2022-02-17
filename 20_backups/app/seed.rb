require 'sequel'
require 'pg'
require 'pry'
require 'benchmark'

sleep 10 # wait for postgres

def insert_rows(table, n: 1_000_000, rows_in_batch: 100)
  counter = 1

  while counter < n do
    rows = (counter..(counter + rows_in_batch)).map do |i|
      category_id = rand(2) + 1

      [category_id, "Author #{category_id}", "Title-#{i}", rand(100) + 1900]
    end

    table.import([:category_id, :author, :title, :year], rows)

    counter += rows_in_batch
  end
end

DB = Sequel.connect('postgres://app:pass@postgres:5432/mydb')

DB.create_table?(:books) do
  primary_key :id
  Integer :category_id, null: false
  String :author, null: false
  String :title, null: false
  Integer :year, null: false

  index :category_id
end

insert_rows(DB[:books], n: 1_000_000, rows_in_batch: 1000) unless DB[:books].first
