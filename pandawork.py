import pandas as pd
import numpy as np
import jinja2

# Sample DataFrame
df = pd.DataFrame(np.random.randn(5, 4), columns=['one', 'two', 'three', 'four'],
                  index=['a', 'b', 'c', 'd', 'e'])

# See: https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Building-styles
def color_negative_red(val):
    color = 'red' if val < 0 else 'black'
    return f'color: {color}'

#styler = df.style.applymap(color_negative_red)

# Template handling
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
print(env)
template = env.get_template('template.html')
print(template)
html = template.render()
print(html,',')

# Plot
ax = df.plot.bar()
fig = ax.get_figure()
fig.savefig('plot.svg')

# Write the HTML file
f = open('report.html', 'w')
f.write(html)
f.close()
