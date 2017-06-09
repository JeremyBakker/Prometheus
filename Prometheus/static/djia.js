var margin = {top: 30, right: 65, bottom: 50, left: 50},
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

d3.tsv('../static/djia.tsv', function(error, data) {
    data.forEach(function(d) {
        d.date = parseTime(d.date);
        d.close = (+d.close).toFixed(2);
        company = d.company
    });

x.domain(d3.extent(data, function(d) { return d.date; }));
y.domain([0, d3.max(data, function(d) { return d.close; })]);

svg.append('path')
    .data([data])
    .attr('class', 'line')
    .attr('class', 'djia')
    .attr('d', valueline);

svg.append('g')
    .attr("class", "axisRight")
    .call(d3.axisRight(y))
    .attr("transform", "translate(" + width + ",0)");

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

    div.html("<span style='color: white'>" + d.company + "<br/>" + formatTime(d.date) + "<br/>" + '$' + d.close + "</span>")
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY - 30) + "px")
        .style("width", "100px")
        .style("height", "50px")
        .style("background-color", "blue");
        })
    .on("mouseout", function(d) {
        div.transition()
        .duration(200)
        .style("opacity", 0)
    });

svg.append("text")             
    .attr("transform",
        "translate(" + (width/2) + " ," + 
        (height + margin.top + 30) + ")")
    .style("text-anchor", "middle")
    .text("Date");

svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", width + (margin.right - 20))
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("fill", "blue")
    .style("text-anchor", "middle")
    .text("Value");

svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Value");  

svg.append("text")
    .attr("transform",
        "translate(" + (width - 100) + " ," + 
        (height + margin.top - 80) + ")")
    .style("text-anchor", "middle")
    .text("Dow Jones Industrial Average");

svg.append("rect")
    .attr("transform",
        "translate(" + (width - 217) + " ," + 
        (height + margin.top - 90) + ")")
    .attr("width", 15)
    .attr("height", 15)
    .attr("fill", "blue")

svg.append("text")
    .attr("transform",
        "translate(" + (width/2) + " ," + 
        (margin.top - 25) + ")")
    .style("text-anchor", "middle")
    .style("font-size", "2em")
    .text("Corporate Earnings Over Time");



});