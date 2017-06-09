var company

d3.tsv('../static/Apple.tsv', function(error, data) {
    data.forEach(function(d) {
        d.date = parseTime(d.date);
        d.close = +d.close;
        company = d.company;
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
        .duration(100)
        .style("opacity", .9);

  formatTime =  d3.timeFormat("%e %B %y");

  div.html(d.company + "<br/>" + formatTime(d.date) + "<br/>" + '$' + d.close)
      .style("left", (d3.event.pageX) + "px")
      .style("top", (d3.event.pageY - 30) + "px")
      .style("width", "100px")
      .style("height", "50px")
      .style("background-color", "white");
    })
  .on("mouseout", function(d) {
        div.transition()
        .duration(200)
        .style("opacity", 0)
  });

svg.append("text")
    .data(data)
    .attr("transform",
        "translate(" + (width - 197) + " ," + 
        (height + margin.top - 57) + ")")
    .html("Corporation: " + company);

svg.append("rect")
    .attr("transform",
        "translate(" + (width - 217) + " ," + 
        (height + margin.top - 70) + ")")
    .attr("width", 15)
    .attr("height", 15)
});