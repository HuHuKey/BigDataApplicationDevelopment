import pandas as pd

html = '''
<tr class="tr-chapter tr-homework">
        <td colspan="4">
                1 大数据概述
            <i class="icon-arrow11"></i>
        </td>
                <td colspan="4">
                2 大数据概述
            <i class="icon-arrow11"></i>
        </td>
    </tr>
'''

from pyquery import PyQuery as pq

col2css = {
    'name': 'div.p-name.p-name-type-2 > a > em',
    'price': 'div.p-price > strong > i',
    'supplier': 'div.p-shop > span > a'
}
q = pq(html)
data_list = dict(zip(col2css.keys(), [[] for _ in col2css.items()]))
data_list['name'] = ['a', 'b', 'c']
data_list['price'] = ['a', 'b', 'c']
data_list['supplier'] = ['a', 'b', 'c']
print(
    pd.DataFrame(data_list).to_dict(orient='records')
)
