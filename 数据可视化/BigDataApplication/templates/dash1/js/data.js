/*各区域产品挂牌数-开始*/
//牧草产能区域分布数据
let DataCenter = [{
    name: "北海数据中心",
    num: "110569"
}, {
    name: "上海数据中心",
    num: "110569"
}, {
    name: "北京数据中心",
    num: "110569"
}, {
    name: "深圳数据中心",
    num: "110569"
}];

/*各区域产品挂牌数-结束*/
//牧草
let ChanNeng = [{
    name: "西南地区销售额",
    num: 891433
}, {
    name: "华南地区销售额",
    num: 189472
}, {
    name: "北方地区销售额",
    num: 63803
}];
//入驻会员实时动态滚动数据
let RZstatus = ["绿邦创景成功挂牌入驻南方草交所", "晨光金品百花园成功挂牌入驻南方草交所", "绿邦创景成功挂牌入驻南方草交所", "晨光金品百花园成功挂牌入", "绿邦创景成功挂牌入驻南方草交所", "晨光金品百花园成功挂牌入驻南方草交所", "绿邦创景成功挂牌入驻南方草交所", "晨光金品百花园成功挂牌入", "绿邦创景成功挂牌入驻南方草交所", "晨光金品百花园成功挂牌入驻南方草交所", "绿邦创景成功挂牌入驻南方草交所", "晨光金品百花园成功挂牌入"];
let callMsg = ["绿邦创景卖出500000万元人民币", "更多模板，关注公众号【DreamCoders】回复'BigDataView'即可获取或前往Gitee下载 https://gitee.com/iGaoWei/big-data-view", "猪猪侠买入500000万元人民币"];

let CJstatus = [];
$.ajax({
    url: 'api/getData',  // 这里替换为实际的请求URL地址
    type: 'POST',
    data: '',
    contentType: 'application/x-www-form-urlencoded',
    success: function (jsonData) {
        // console.log(jsonData)
        jsonData.forEach(sale => {
            let item = [{
                commentNum: sale.commentCnt,
                name: sale.name,
                price: sale.price,
                totalSale: sale.grossSales,
                supplier: sale.supplier,
                href: sale.href
            }];
            // console.log(item)
            CJstatus.push(item);
        });
        for (var i = 0; i < CJstatus[1].length; i++) {
            $(".liushuihaoul .moveul").html((index, html) => {
                return html += `<li>
				<span>${CJstatus[1][i].commentNum}</span>
				<span>${CJstatus[1][i].name}</span>
				<span>${CJstatus[1][i].price}</span>
				<span>${CJstatus[1][i].totalSale}</span>
				<span>${CJstatus[1][i].supplier}</span>
				<span>${CJstatus[1][i].href}</span>
				</li>`
            })
        }


    },
    error: function (jqXHR, textStatus, errorThrown) {
        // console.error(textStatus + ": " + errorThrown);
        // var html = "出错啦,请检查输入" + jqXHR.responseText;
        // $('#result').html(html);
    }
});
