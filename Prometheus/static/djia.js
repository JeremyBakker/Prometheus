// This script renders the D3 svg, the x axis and label, the left y-axis and
// label, and the line graph for the Dow Jones Industrial Average.

var margin = {top: 30, right: 65, bottom: 70, left: 60},
    width = 860 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var parseTime = d3.timeParse('%d-%b-%y');

var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

var valueline = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close) });

var svg = d3.select('#valueChart').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 
            'translate(' + margin.left + ',' + margin.top + ')');

var div = d3.select("body").append("div")
.attr("class", "tooltip")
.style("opacity", 0);

var company

d3.tsv('../static/data/djia.tsv', function(error, data) {
    data.forEach(function(d) {
        d.date = parseTime(d.date);
        d.close = Math.round(+d.close);
        company = d.company
    });

x.domain(d3.extent(data, function(d) { return d.date; }));
y.domain([0, d3.max(data, function(d) { 
    return d.close; })]);

svg.append('path')
    .data([data])
    .attr('class', 'line')
    .attr('class', 'djia')
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
    .attr("class", "axisLeft")
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
        .duration(100)
        .style("opacity", .9);

    formatTime =  d3.timeFormat("%e %B %y");

    div.html("<span style='color: black'>" + d.company + "<br/>" + formatTime(d.date) + "<br/>" + '$' + d.close + "</span>")
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY - 30) + "px")
        .style("width", "110px")
        .style("height", "50px")
        .style("background-color", "white");
        })
    .on("mouseout", function(d) {
        div.transition()
        .duration(200)
        .style("opacity", 0)
    });

svg.append("text")             
    .attr("transform",
        "translate(" + (width/2) + " ," + 
        (height + margin.top + 25) + ")")
    .style("text-anchor", "middle")
    .style("font-size", ".8em")
    .text("Date");

svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("fill", "black")
    .style("text-anchor", "middle")
    .style("font-size", ".8em")
    .text("Value in U.S. Dollars");  

svg.append("text")
    .attr("transform",
        "translate(" + (width - 106) + " ," + 
        (height + margin.top - 78) + ")")
    .style("text-anchor", "middle")
    .style("font-size", ".8em")
    .text("Dow Jones Industrial Average");

svg.append("rect")
    .attr("transform",
        "translate(" + (width - 217) + " ," + 
        (height + margin.top - 90) + ")")
    .attr("width", 15)
    .attr("height", 15)
    .attr("fill", "black")

svg.append("text")
    .attr("transform",
        "translate(" + (width - 266) + " ," + 
        (height + margin.top - 40) + ")")
    .style("text-anchor", "middle")
    .style("font-size", ".8em")
    .text("*  Earnings numbers in the tooltip have been rounded to the nearest whole number.");

svg.append("text")
    .attr("transform",
        "translate(" + (width/2) + " ," + 
        (margin.top - 35) + ")")
    .style("text-anchor", "middle")
    .style("font-size", "2em")
    .text("Corporate Earnings Over Time*");
});