var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseTime = d3.timeParse('%d-%b-%y');

var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

var valueline = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close) });

var svg = d3.select('body').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
    .append('g')
        .attr('transform', 
            'translate(' + margin.left + ',' + margin.top + ')');

var div = d3.select("body").append("div")
.attr("class", "tooltip")
.style("opacity", 0);

d3.tsv('../static/Apple.tsv', function(error, data) {
    data.forEach(function(d) {
        d.date = parseTime(d.date);
        d.close = +d.close;
    });

x.domain(d3.extent(data, function(d) { return d.date; }));
y.domain([0, d3.max(data, function(d) { return d.close; })]);

svg.append('path')
    .data([data])
    .attr('class', 'line')
    .attr('d', valueline);

svg.append("g")
  .attr("class", "axis axis--x")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .selectAll("text")
  .attr("y", 0)
  .attr("x", 9)
  .attr("dy", ".35em")
  .attr("transform", "rotate(45)")
  .style("text-anchor", "start");

svg.append('g')
    .call(d3.axisLeft(y));

svg.selectAll("dot")
    .data(data)
    .enter().append("circle")
    .attr("r", 5)
    .attr("cx", function(d) { return x(d.date); })
    .attr("cy", function(d) { return y(d.close); })
    .attr('opacity', 0)
    .on("mouseover", function(d) {
        div.transition()
        .duration(200)
        .style("opacity", .9);

formatTime =  d3.timeFormat("%e %B %y");
div.html(formatTime(d.date) + "<br/>" + '$' + d.close)
    .style("left", (d3.event.pageX) + "px")
    .style("top", (d3.event.pageY - 30) + "px")
    .style("width", "100px");
    })
});