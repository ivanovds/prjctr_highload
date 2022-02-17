import plotext as plt

x = []
x.append(    201)
x.append(    401)
x.append(    801)
x.append(   1601)
x.append(   3201)
x.append(   6401)
x.append(  12801)
x.append(  25601)
x.append(  51201)

y = []
y.append(0.002)
y.append(0.004)
y.append(0.007)
y.append(0.009)
y.append(0.030)
y.append(0.050)
y.append(0.081)
y.append(0.159)
y.append(0.289)

plt.scatter(y)
plt.title("Scatter Plot")
plt.show()