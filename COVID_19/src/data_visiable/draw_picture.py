import pyecharts.options as opts
from pyecharts.charts import Line, Geo, Map, Parallel, Scatter, Bar, Pie, Grid, Radar, TreeMap, HeatMap, ThemeRiver
# from pyecharts_snapshot.main import make_a_snapshot
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot


def to_svg(file_name, svg_name):
    a = '<script>'
    b = """<a id="download" href="">下载</a>
            <script type="text/javascript" >
            const a = window.document.querySelector('#download');
          a.addEventListener('click',()=>{
        const content = document.querySelector('svg').outerHTML
        const blob= new Blob([content], {type: 'xml/svg'})
        a.href = URL.createObjectURL(blob)
        a.download = '%s.svg'
  })
    """ % file_name.split('/')[-1].split('.')[0]
    # 读取文件
    f = open(file_name, "r", encoding="utf-8")
    data = f.read()
    f.close()
    data = data.replace(a, b)
    data = data.replace('canvas', 'svg')
    f = open(svg_name, 'w', encoding="utf-8")
    f.write(data)
    f.close()


def draw_line_with_two_y(xaxis_data, y1_series_name, y1_axis, y2_series_name, y2_axis, y3_series_name, y3_axis,
                         y1_name, y2_name, to_file, unit, svg_name):
    """
    左边是  两条线； 右边是 一条线。
    :param svg_name: svg文件
    :param xaxis_data: 横轴
    :param y1_series_name: 左边第一条线的系列名
    :param y1_axis: 左边第一条线的数值
    :param y2_series_name: 左边第二条线的系列名
    :param y2_axis: 左边第二条线的数值
    :param y3_series_name: 右边第一条线的系列名
    :param y3_axis: 右边第一条线的数值
    :param y1_name: 左边的纵轴名称
    :param y2_name: 右边的纵轴名称
    :param to_file: 结果文件
    :param unit: 横轴的数值的单位（加在每个横轴值后面，比如 月）
    :return:
    """
    xaxis_data = [str(i) + unit for i in xaxis_data]
    bar = Line(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')
               ).add_xaxis(
        xaxis_data=xaxis_data,
        # add_xaxis=opts.LabelOpts(formatter="{value}" + unit),
    ).add_yaxis(
        series_name=y1_series_name,
        is_smooth=True,
        symbol="circle",
        symbol_size=8,
        is_symbol_show=True,
        # color="#d14a61",
        y_axis=y1_axis,
        yaxis_index=0,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=2),
    ).add_yaxis(
        series_name=y2_series_name,
        is_smooth=True,
        symbol="circle",
        symbol_size=8,
        is_symbol_show=True,
        # color="#d14a61",
        y_axis=y2_axis,
        yaxis_index=0,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=2),
    ).add_yaxis(
        series_name=y3_series_name,
        is_smooth=True,
        symbol="circle",
        symbol_size=8,
        is_symbol_show=True,
        # color="#d14a61",
        y_axis=y3_axis,
        yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=2),
    ).extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name=y2_name,
            # min_=0,
            # max_=25,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=15),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
            name_textstyle_opts=opts.TextStyleOpts(font_size=15)
        )
    ).set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name=y1_name,
            # min_=0,
            # max_=250,
            position="left",
            offset=0,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=15),
            name_textstyle_opts=opts.TextStyleOpts(font_size=15)
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=15),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
            )
        ),
        legend_opts=opts.LegendOpts(item_width=25,
                                    item_height=10,
                                    textstyle_opts=opts.TextStyleOpts(font_size=15)),
    )
    make_snapshot(snapshot, bar.render(to_file), svg_name)  # 生成svg图片


def draw_map_world(data, to_file, svg_name, label_name, number_max):
    """
    画地图
    :param data:
    :param to_file:
    :param svg_name:
    :param label_name: 图例名称
    :param number_max: 最大值
    :return:
    """
    geo = Map(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='rgb(255, 255, 255)')) \
        .add(label_name, data, maptype="world") \
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                         showLegendSymbol=False) \
        .set_global_opts(legend_opts=opts.LegendOpts(item_width=50,
                                                     item_height=30,
                                                     textstyle_opts=opts.TextStyleOpts(font_size=30)),
                         visualmap_opts=opts.VisualMapOpts(min_=0,
                                                           max_=int(number_max),
                                                           background_color='rgb(255, 255, 255)',
                                                           is_piecewise=True,
                                                           item_width=50,
                                                           item_height=30,
                                                           textstyle_opts=opts.TextStyleOpts(font_size=30)),
                         toolbox_opts=opts.ToolboxOpts(
                             feature=opts.ToolBoxFeatureOpts(
                                 data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                 # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
                             )
                         ),
                         )
    # geo.render(to_file)
    make_snapshot(snapshot, geo.render(to_file), svg_name)  # 生成svg图片


def draw_rank_change(axis_name_list, axis_data, data, to_file, svg_name):
    """
    平行坐标系
    :param axis_name_list:
    :param axis_data: 是str才行哦
    :param data: 格式 [[name, result],[name, result]] result 是 [[这里是值]] 的格式
    :param to_file:
    :param svg_name:
    :return:
    """
    # 设置schema
    parallel_axis = []
    for i in range(len(axis_name_list)):
        one_dict = {'dim': i,
                    'name': axis_name_list[i],
                    'type': 'category',
                    'data': axis_data,
                    'inverse': True,
                    'nameTextStyle': opts.TextStyleOpts(font_size=15),
                    'axisLabel': opts.LabelOpts(font_size=15)
                    }
        parallel_axis.append(one_dict)
    # 设置结果
    p = Parallel(init_opts=opts.InitOpts(width="900px", height="600px", bg_color='White')) \
        .add_schema(schema=parallel_axis,
                    parallel_opts=opts.ParallelOpts(pos_top='5%',
                                                    pos_right='20%',
                                                    pos_left='10%',
                                                    )
                    )
    for i in range(len(data)):
        p = p.add(series_name=data[i][0],
                  data=data[i][1],
                  linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
                  is_smooth=True,
                  )
    p = p.set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="85%", pos_top="18%",
                                                      orient="vertical", backgroundColor='rgb(255, 255, 255)',
                                                      item_width=25,
                                                      item_height=15,
                                                      textstyle_opts=opts.TextStyleOpts(font_size=15)
                                                      ),
                          tooltip_opts=opts.TooltipOpts(position="right"),
                          toolbox_opts=opts.ToolboxOpts(),
                          )
    make_snapshot(snapshot, p.render(to_file), svg_name)  # 生成svg图片


def draw_triple_rank_scatter(x_list, y_list, data, html_file_name):
    """
    排名散点图（点的大小全部相同）
    :param x_list: list[str] x轴
    :param y_list: list[str] y轴
    :param data: data  {series_name: [[横坐标，纵坐标，值],[横坐标，纵坐标，值]]}
    :param html_file_name:
    :return:
    """

    series = '['
    for key, data_one in data.items():
        series_data = []
        series_str = '''{name: "''' + str(key) + '''", 
                type: 'scatter',
                symbolSize: function(val) {
            return Math.sqrt(80)*5;},
            data:
            '''
        for data_one_one in data_one:
            series_data.append([data_one_one[1], data_one_one[0], data_one_one[2]])
        series = series + series_str + str(series_data) + '},'
    series = series[:-1] + "]"

    result = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>ECharts</title>
            <!-- 引入 echarts.js -->
            <script src="echarts.js"></script>
        </head>
        <body>
            <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
            <div id="main" style="width: 800px;height:600px;"></div>
            <a id="download" href="">下载</a>
            <script type="text/javascript" >
            const a = window.document.querySelector('#download');
          a.addEventListener('click',()=>{
        const content = document.querySelector('svg').outerHTML
        const blob= new Blob([content], {type: 'xml/svg'})
        a.href = URL.createObjectURL(blob)
        a.download = '散点图.svg'
  })
                // 基于准备好的dom，初始化echarts实例
                var myChart = echarts.init(document.getElementById('main'), 'white', {renderer: 'svg'});
        var hours = """ + str(x_list) + '; var days = ' + str(y_list) + """ ;
            option = {
            backgroundColor: "rgb(255, 255, 255)",
            title: {
                text: '',
            },
            legend: {
                data: """ + str(list(data.keys())) + """,
                left: 'right',
                backgroundColor: "rgb(255, 255, 255)",
            },
            tooltip: {
                position: 'top',
                formatter: function (params) {
                    return hours[params.value[0]] + ' : ' +  days[params.value[1]] ;
                }
            },
            grid: {
                left: '20%',
                bottom: '5%',
                right: '10%',
                top: '10%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: hours,
                boundaryGap: false,
                 axisLabel :{
                    interval : 0,
                    rotate : '0'
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: '#ddd',
                        type: 'dashed'
                    }
                },
                axisLine: {
                    show: false
                }
            },
            yAxis: {
                type: 'category',
                axisLabel :{
                    interval : 0,
                    left: '5%',
                },
                data: days,
                axisLine: {
                    show: false
                },
                
                
            },
            series: """ + series + """
        };

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
            </script>
        </body>
        </html>
                 """

    out = open(html_file_name, 'w', encoding="utf-8")
    out.write(result)
    out.close()


def draw_line_picture(xaxis_data, data, to_file, unit, svg_name, stack, y_name):
    """
    多条线，是否堆叠要确认下
    :param label_right:
    :param y_name: y轴名称
    :param stack: boolean, 是否要堆叠
    :param xaxis_data: x轴
    :param data: {series_name, data}
    :param svg_name: svg文件
    :param to_file: 结果文件
    :param unit: 横轴的数值的单位（加在每个横轴值后面，比如 月）
    :return:
    """
    xaxis_data = [str(i) + unit for i in xaxis_data]
    bar = Line(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')
               ).add_xaxis(
        xaxis_data=xaxis_data,
        # add_xaxis=opts.LabelOpts(formatter="{value}" + unit),
    )
    for series_name, y_axis in data.items():
        if stack:
            bar = bar.add_yaxis(
                series_name=series_name,
                is_smooth=True,
                symbol="circle",
                # symbol_size=8,
                stack='1',
                is_symbol_show=False,
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                # linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(opacity=1)
            )
        else:
            bar = bar.add_yaxis(
                series_name=series_name,
                is_smooth=True,
                symbol="circle",
                symbol_size=8,
                is_symbol_show=True,
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(width=2),
            )
    bar = bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name=y_name,
            name_textstyle_opts=opts.TextStyleOpts(font_size=25),
            # min_=0,
            # max_=250,
            position="left",
            offset=0,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=25),
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=25, interval=0),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
            )
        ),
        legend_opts=opts.LegendOpts(pos_left="12%",
                                    pos_top="10%",
                                    orient="vertical",
                                    # backgroundColor='rgb(255, 255, 255)',
                                    item_width=40,
                                    item_height=20,
                                    textstyle_opts=opts.TextStyleOpts(font_size=25)
                                    ),
    )
    make_snapshot(snapshot, bar.render(to_file), svg_name)  # 生成svg图片


def draw_river_picture(series_name, data, to_file, svg_name):
    """
    主题河流图
    :param series_name: [str]
    :param data: [[date, value, series_name]]
    :param svg_name: svg文件
    :param to_file: 结果文件
    :return:
    """
    bar = ThemeRiver(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')) \
        .add(
        series_name=series_name,
        data=data,
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="2%",
            pos_bottom="10%",
            pos_right="20%",
            type_="time",
            name_textstyle_opts=opts.TextStyleOpts(font_size=25),
            axislabel_opts=opts.LabelOpts(font_size=25)
        ),
        label_opts=opts.LabelOpts(is_show=False, position='bottom', distance='200px'),
    ) \
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                # data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
            )
        ),
        legend_opts=opts.LegendOpts(type_="scroll",
                                    pos_left="82%",
                                    pos_top="18%",
                                    orient="vertical",
                                    backgroundColor='rgb(255, 255, 255)',
                                    item_width=40,
                                    item_height=20,
                                    textstyle_opts=opts.TextStyleOpts(font_size=25)
                                    )
    )
    make_snapshot(snapshot, bar.render(to_file), svg_name)  # 生成svg图片


def draw_triple_number_scatter(x_list, y_list, data, html_file_name, size, y_name):
    """
        散点图
        :param y_name: y轴名称
        :param size: 要乘的倍数
        :param x_list: list[str] x轴
        :param y_list: list[str] y轴
        :param data: data  {series_name: [[横坐标，纵坐标，值],[横坐标，纵坐标，值]]}
        :param html_file_name:
        :return:
    """

    series = '['
    for key, data_one in data.items():
        series_data = []
        series_str = '''{name: "''' + str(key) + '''", 
                type: 'scatter',
                symbolSize: function(val) {
            return Math.sqrt(val[2])*''' + str(size) + ''';},
            data:
            '''
        for data_one_one in data_one:
            series_data.append([data_one_one[1], data_one_one[0], data_one_one[2]])
        series = series + series_str + str(series_data) + '},'
    series = series[:-1] + "]"

    result = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>ECharts</title>
            <!-- 引入 echarts.js -->
            <script src="echarts.js"></script>
        </head>
        <body>
            <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
            <div id="main" style="width: 800px;height:600px;"></div>
            <script type="text/javascript" >          
                // 基于准备好的dom，初始化echarts实例
                var myChart = echarts.init(document.getElementById('main'), 'white', {renderer: 'png'});
        var hours = """ + str(x_list) + '; var days = ' + str(y_list) + """ ;
            option = {
            backgroundColor: "rgb(255, 255, 255)",
            title: {
                text: '',
            },
            legend: {
                data: """ + str(list(data.keys())) + """,
                left: 'right',
                show: false,
                backgroundColor: "rgb(255, 255, 255)",
            },
             "toolbox": {
        "show": true,
        "orient": "horizontal",
        "itemSize": 15,
        "itemGap": 10,
        "left": "80%",
        "feature": {
            "saveAsImage": {
                "type": "png",
                "backgroundColor": "auto",
                "connectedBackgroundColor": "#fff",
                "show": true,
                "title": "\u4fdd\u5b58\u4e3a\u56fe\u7247",
                "pixelRatio": 1
            },
            "restore": {
                "show": true,
                "title": "\u8fd8\u539f"
            },
            "dataView": {
                "show": true,
                "title": "\u6570\u636e\u89c6\u56fe",
                "readOnly": false,
                "lang": [
                    "\u6570\u636e\u89c6\u56fe",
                    "\u5173\u95ed",
                    "\u5237\u65b0"
                ],
                "backgroundColor": "#fff",
                "textareaColor": "#fff",
                "textareaBorderColor": "#333",
                "textColor": "#000",
                "buttonColor": "#c23531",
                "buttonTextColor": "#fff"
            },
            "dataZoom": {
                "show": false,
                "title": {
                    "zoom": "\u533a\u57df\u7f29\u653e",
                    "back": "\u533a\u57df\u7f29\u653e\u8fd8\u539f"
                },
                "icon": {},
                "xAxisIndex": false,
                "yAxisIndex": false,
                "filterMode": "filter"
            },
            "magicType": {
                "show": true,
                "type": [
                    "line",
                    "bar",
                    "stack",
                    "tiled"
                ],
                "title": {
                    "line": "\u5207\u6362\u4e3a\u6298\u7ebf\u56fe",
                    "bar": "\u5207\u6362\u4e3a\u67f1\u72b6\u56fe",
                    "stack": "\u5207\u6362\u4e3a\u5806\u53e0",
                    "tiled": "\u5207\u6362\u4e3a\u5e73\u94fa"
                },
                "icon": {}
            },
            "brush": {
                "icon": {},
                "title": {
                    "rect": "\u77e9\u5f62\u9009\u62e9",
                    "polygon": "\u5708\u9009",
                    "lineX": "\u6a2a\u5411\u9009\u62e9",
                    "lineY": "\u7eb5\u5411\u9009\u62e9",
                    "keep": "\u4fdd\u6301\u9009\u62e9",
                    "clear": "\u6e05\u9664\u9009\u62e9"
                }
            }
        }
    }
,
            'tooltip': {
                position: 'top',
                formatter: function (params) {
                    return hours[params.value[0]] + ' - ' +  days[params.value[1]] + ': ' +  params.value[2] ;
                }
            },
            grid: {
                left: '10%',
                bottom: '5%',
                right: '10%',
                top: '10%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: hours,
                boundaryGap: false,
                axisLabel :{
                    interval : 0,
                    rotate : '0',
                    fontSize:25,
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: '#ddd',
                        type: 'dashed'
                    }
                },
                axisLine: {
                    show: false
                },
                
            },
            yAxis: {
                type: 'category',
                axisLabel :{
                    interval : 0,
                    left: '5%',
                    fontSize:25,
                },
                name: '""" + str(y_name) + """',
                data: days,
                axisLine: {
                    show: false
                },
                nameTextStyle:{
                    fontSize:25,
                }


            },
            series: """ + series + """
        };

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
            </script>
        </body>
        </html>
                 """

    out = open(html_file_name, 'w', encoding="utf-8")
    out.write(result)
    out.close()


def draw_bar_picture(xaxis_data, data, to_file, unit, svg_name, stack, y_name):
    """
    多个y列，是否堆叠要确认下
    :param is_reverse: xy轴是否反转
    :param y_name: y轴名称
    :param stack: boolean, 是否要堆叠
    :param xaxis_data: x轴
    :param data: {series_name, data}
    :param svg_name: svg文件
    :param to_file: 结果文件
    :param unit: 横轴的数值的单位（加在每个横轴值后面，比如 月）
    :return:
    """
    xaxis_data = [str(i) + unit for i in xaxis_data]
    bar = Bar(init_opts=opts.InitOpts(width="900px", height="600px", bg_color='white')
              ).add_xaxis(
        xaxis_data=xaxis_data,
        # add_xaxis=opts.LabelOpts(formatter="{value}" + unit),
    )
    for series_name, y_axis in data.items():
        if stack:
            bar = bar.add_yaxis(
                series_name=series_name,
                stack='1',
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
        else:
            bar = bar.add_yaxis(
                series_name=series_name,
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
    bar = bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name=y_name,
            name_textstyle_opts=opts.TextStyleOpts(font_size=15),
            # min_=0,
            # max_=250,
            position="left",
            offset=0,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=15),
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=15, interval=0),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
            )
        ),
        legend_opts=opts.LegendOpts(item_width=25,
                                    item_height=15,
                                    textstyle_opts=opts.TextStyleOpts(font_size=15)
                                    ),
    )
    make_snapshot(snapshot, bar.render(to_file), svg_name)  # 生成svg图片


def draw_pie_picture(data, to_file, svg_name, colors=None):
    c = Pie(init_opts=opts.InitOpts(width="1600px", height="900px", bg_color='white')) \
        .add("", data) \
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                         toolbox_opts=opts.ToolboxOpts(is_show=True)) \
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=25)) \
        .set_colors(colors)
    make_snapshot(snapshot, c.render(to_file), svg_name)  # 生成svg图片


def draw_bar_reverse_picture(xaxis_data, data, to_file, unit, svg_name, stack, y_name, pos_left='25%'):
    """
    多个y列，是否堆叠要确认下
    :param pos_left: "25%"
    :param is_reverse: xy轴是否反转
    :param y_name: y轴名称
    :param stack: boolean, 是否要堆叠
    :param xaxis_data: x轴
    :param data: {series_name, data}
    :param svg_name: svg文件
    :param to_file: 结果文件
    :param unit: 横轴的数值的单位（加在每个横轴值后面，比如 月）
    :return:
    """
    xaxis_data = [str(i) + unit for i in xaxis_data]
    bar = Bar(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')).add_xaxis(  # 1250px
        xaxis_data=xaxis_data,
        # add_xaxis=opts.LabelOpts(formatter="{value}" + unit),
    )
    for series_name, y_axis in data.items():
        if stack:
            bar = bar.add_yaxis(
                series_name=series_name,
                stack='1',
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
        else:
            bar = bar.add_yaxis(
                series_name=series_name,
                color="#61a0a8",
                category_gap='50%',
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=True, position='right'),
            )
    bar = bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="category",
            # min_=0,
            # max_=250,
            position="left",
            offset=0,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=20),
        ),
        xaxis_opts=opts.AxisOpts(
            name=y_name,
            name_textstyle_opts=opts.TextStyleOpts(font_size=20),
            axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=20),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
            )
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    bar = bar.reversal_axis()
    grid = (
        Grid(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='rgb(255, 255, 255)'))  # 800px
            .add(bar, grid_opts=opts.GridOpts(pos_left=pos_left), is_control_axis_index=True)
    )
    make_snapshot(snapshot, grid.render(to_file), svg_name)  # 生成svg图片


def draw_line_picture_right_legend(xaxis_data, data, to_file, unit, svg_name, stack, y_name, pos_right, width='800px'):
    """
    多条线，是否堆叠要确认下
    :param width:
    :param pos_right:
    :param y_name: y轴名称
    :param stack: boolean, 是否要堆叠
    :param xaxis_data: x轴
    :param data: {series_name, data}
    :param svg_name: svg文件
    :param to_file: 结果文件
    :param unit: 横轴的数值的单位（加在每个横轴值后面，比如 月）
    :return:
    """
    xaxis_data = [str(i) + unit for i in xaxis_data]
    bar = Line(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')
               ).add_xaxis(
        xaxis_data=xaxis_data,
        # add_xaxis=opts.LabelOpts(formatter="{value}" + unit),
    )
    for series_name, y_axis in data.items():
        if stack:
            bar = bar.add_yaxis(
                series_name=series_name,
                is_smooth=True,
                symbol="circle",
                # symbol_size=8,
                stack='1',
                is_symbol_show=False,
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                # linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(opacity=1)
            )
        else:
            bar = bar.add_yaxis(
                series_name=series_name,
                is_smooth=True,
                symbol="circle",
                symbol_size=8,
                is_symbol_show=True,
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(width=2),
            )
    bar = bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name=y_name,
            # min_=0,
            # max_=250,
            position="left",
            offset=0,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(
        #     feature=opts.ToolBoxFeatureOpts(
        #         data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
        #         # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
        #     )
        # ),
        legend_opts=opts.LegendOpts(pos_right='10%', pos_top="2%", orient="vertical"),
    )
    grid = (
        Grid(init_opts=opts.InitOpts(width=width, height="600px", bg_color='rgb(255, 255, 255)'))
            .add(bar, grid_opts=opts.GridOpts(pos_right=pos_right), is_control_axis_index=True)
    )
    grid.render(to_file)
    to_svg(to_file, svg_name)


def draw_river_picture_right_legend(series_name, data, to_file, svg_name, pos_right, width='800px'):
    """
    主题河流图
    :param width:
    :param pos_right:
    :param series_name: [str]
    :param data: [[date, value, series_name]]
    :param svg_name: svg文件
    :param to_file: 结果文件
    :return:
    """
    bar = ThemeRiver(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')) \
        .add(
        series_name=series_name,
        data=data,
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="50",
            pos_bottom="50",
            type_="time",
            name_textstyle_opts=opts.TextStyleOpts(font_size=20),
            axislabel_opts=opts.LabelOpts(font_size=20)
        ),
        label_opts=opts.LabelOpts(is_show=False),
    ) \
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
            )
        ),
        legend_opts=opts.LegendOpts(pos_right=pos_right,
                                    pos_top="2%",
                                    orient="vertical",
                                    item_width=30,
                                    item_height=14,
                                    textstyle_opts=opts.TextStyleOpts(font_size=18)
                                    ),
    )
    grid = (
        Grid(init_opts=opts.InitOpts(width=width, height="600px", bg_color='rgb(255, 255, 255)'))
            .add(bar, grid_opts=opts.GridOpts(pos_right='10%'), is_control_axis_index=True)
    )
    make_snapshot(snapshot, grid.render(to_file), svg_name)  # 生成svg图片


def draw_bar_picture_right_legend(xaxis_data, data, to_file, unit, svg_name, stack, y_name, pos_right, width='800px'):
    """
    多个y列，是否堆叠要确认下
    :param width:
    :param pos_right:
    :param is_reverse: xy轴是否反转
    :param y_name: y轴名称
    :param stack: boolean, 是否要堆叠
    :param xaxis_data: x轴
    :param data: {series_name, data}
    :param svg_name: svg文件
    :param to_file: 结果文件
    :param unit: 横轴的数值的单位（加在每个横轴值后面，比如 月）
    :return:
    """
    xaxis_data = [str(i) + unit for i in xaxis_data]
    bar = Bar(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')
              ).add_xaxis(
        xaxis_data=xaxis_data,
        # add_xaxis=opts.LabelOpts(formatter="{value}" + unit),
    )
    for series_name, y_axis in data.items():
        if stack:
            bar = bar.add_yaxis(
                series_name=series_name,
                stack='1',
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
        else:
            bar = bar.add_yaxis(
                series_name=series_name,
                # color="#d14a61",
                y_axis=y_axis,
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
    bar = bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name=y_name,
            # min_=0,
            # max_=250,
            position="left",
            offset=0,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(
        #     feature=opts.ToolBoxFeatureOpts(
        #         data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
        #         # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
        #     )
        # ),
        legend_opts=opts.LegendOpts(pos_right='10%', pos_top="2%", orient="vertical"),
    )

    grid = (
        Grid(init_opts=opts.InitOpts(width=width, height="600px", bg_color='rgb(255, 255, 255)'))
            .add(bar, grid_opts=opts.GridOpts(pos_right=pos_right), is_control_axis_index=True)
    )
    grid.render(to_file)
    to_svg(to_file, svg_name)


def draw_radar_picture(data, indicator, html_file_name):
    """
    画雷达图
    :param data: ｛serise_name: [value]｝
    :param indicator: [{text, max}] 的格式
    :param html_file_name:
    :return:
    """
    indicator[0]['axisLabel'] = {'show': 'true'}
    series = {'type': 'radar'}
    series_data = []
    for key, value in data.items():
        series_data.append({'name': key, 'value': value, 'areaStyle': {}})
    series['data'] = series_data
    series = str(series)

    result = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>ECharts</title>
                <!-- 引入 echarts.js -->
                <script src="echarts.js"></script>
            </head>
            <body>
                <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
                <div id="main" style="width: 800px;height:600px;"></div>
                <a id="download" href="">下载</a>
                <script type="text/javascript" >
                const a = window.document.querySelector('#download');
              a.addEventListener('click',()=>{
            const content = document.querySelector('svg').outerHTML
            const blob= new Blob([content], {type: 'xml/svg'})
            a.href = URL.createObjectURL(blob)
            a.download = '雷达图.svg'
      })
                    // 基于准备好的dom，初始化echarts实例
                    var myChart = echarts.init(document.getElementById('main'), 'white', {renderer: 'svg'});
                option = {
                    "backgroundColor": "rgb(255, 255, 255)",
                title: {
                    text: '',
                },
                legend: {
                    data: """ + str(list(data.keys())) + """,
                    left: 'right',
                    backgroundColor: "rgb(255, 255, 255)",
                },
                tooltip: {
                    position: 'top',
                },
                grid: {
                    left: '20%',
                    bottom: '5%',
                    right: '10%',
                    top: '10%',
                    containLabel: true,
                    backgroundColor: "rgb(255, 255, 255)",
                },
                radar: {
                    indicator: """ + str(indicator) + """,
                    radius: 190,
                    center: ['50%', '60%'],
                    name: {
                        textStyle: {
                            color: '#8D532E'
                        }
                    },
                    splitArea: {
                        areaStyle: {
                            color: ['rgb(255, 255, 255)']
                        }
                    },

                },
                series: """ + series + """
            };

                    // 使用刚指定的配置项和数据显示图表。
                    myChart.setOption(option);
                </script>
            </body>
            </html>
                     """

    out = open(html_file_name, 'w', encoding="utf-8")
    out.write(result)
    out.close()


def draw_tree_picture(data, to_file, svg_name, colors=None):
    c = TreeMap(init_opts=opts.InitOpts(width="800px", height="600px", bg_color='white')) \
        .add("", data) \
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False), ) \
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", position='top'))
    c.render(to_file)
    to_svg(to_file, svg_name)


def draw_heat_map_picture(grid_data, x_list, max_number, to_file, svg_name, height='1200px'):
    """
    grid堆叠热力图
    :param height:
    :param x_list: 横轴列表
    :param max_number: 最大值
    :param grid_data: [{}] key包括 series_name, y_name, sub_title, value
    :param to_file:
    :param svg_name:
    :return:
    """
    grid_number = len(grid_data)
    grid = (Grid(init_opts=opts.InitOpts(width="900px", height=height, bg_color='rgb(255, 255, 255)')))

    i = 0
    all_top = 5
    for grid_data_one in grid_data:
        # max_number_list = [i[2] for i in grid_data_one['value'][3:]]
        # max_number = max(max_number_list)
        length = int(len(grid_data_one['y_name']))*1.5
        top_position = all_top
        bottom_position = 100 - top_position - length
        all_top = top_position + length + 2
        # print(top_position)
        # print(bottom_position)
        # print(all_top)
        c = HeatMap() \
            .add_xaxis(x_list) \
            .add_yaxis(grid_data_one['series_name'], grid_data_one['y_name'], grid_data_one['value'],
                       label_opts=opts.LabelOpts(is_show=True, position="inside"),
                       )
        if i == grid_number - 1:
            c = c.set_global_opts(
                title_opts=opts.TitleOpts(title="",
                                          subtitle=grid_data_one['sub_title'],
                                          pos_top=str(top_position) + "%", ),
                visualmap_opts=opts.VisualMapOpts(is_show=False,
                                                  min_=0,
                                                  max_=
                                                  max_number,
                                                  range_color=['#fff799', '#ae4130']
                                                  ),
                xaxis_opts=opts.AxisOpts(is_show=True,
                                         axislabel_opts=opts.LabelOpts(interval=0, rotate=30),
                                         splitarea_opts=opts.SplitAreaOpts(is_show=False,
                                                                           areastyle_opts=opts.AreaStyleOpts(opacity=0)
                                                                           )
                                         ),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=14, interval=0),
                                         splitarea_opts=opts.SplitAreaOpts(is_show=False,
                                                                           areastyle_opts=opts.AreaStyleOpts(opacity=0)
                                                                           )
                                         ),
                legend_opts=opts.LegendOpts(pos_top="120%"),
                toolbox_opts=opts.ToolboxOpts(
                    feature=opts.ToolBoxFeatureOpts(
                        data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                        # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
                    )
                ),
            )
        else:
            c = c.set_global_opts(
                title_opts=opts.TitleOpts(title="",
                                          subtitle=grid_data_one['sub_title'],
                                          pos_top=str(top_position - 2) + "%", ),
                visualmap_opts=opts.VisualMapOpts(is_show=False,
                                                  min_=0,
                                                  max_=
                                                  max_number,
                                                  range_color=['#fff799', '#ae4130']
                                                  ),
                xaxis_opts=opts.AxisOpts(is_show=False,
                                         splitarea_opts=opts.SplitAreaOpts(is_show=False,
                                                                           areastyle_opts=opts.AreaStyleOpts(opacity=0)
                                                                           )
                                         ),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=14, interval=0),
                                         splitarea_opts=opts.SplitAreaOpts(is_show=False,
                                                                           areastyle_opts=opts.AreaStyleOpts(opacity=0)
                                                                           )
                                         ),
                legend_opts=opts.LegendOpts(pos_top="120%"),
                toolbox_opts=opts.ToolboxOpts(
                    feature=opts.ToolBoxFeatureOpts(
                        data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                        # brush=opts.ToolBoxFeatureBrushOpts(is_show=False),
                    )
                ),
            )
        # 加到grid
        grid = grid.add(c,
                        grid_opts=opts.GridOpts(pos_bottom=str(bottom_position) + "%",
                                                pos_top=str(top_position) + "%",
                                                pos_left="25%",
                                                pos_right="10%"))
        i = i + 1

    make_snapshot(snapshot, grid.render(to_file), svg_name)  # 生成svg图片
