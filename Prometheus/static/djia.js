d3.tsv('../static/djia.tsv', function(error, data) {
    data.forEach(function(d) {
        d.date = parseTime(d.date);
        d.close = +d.close;
    });

x.domain(d3.extent(data, function(d) { return d.date; }));
y.domain([0, d3.max(data, function(d) { return d.close; })]);

svg.append('path')
    .data([data])
    .attr('class', 'line')
    .attr('class', 'djia')
    .attr('d', valueline);

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