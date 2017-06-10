$("#AAPL").click(function (event) {
    console.log("click!");
    showCorporationChart("Apple");
    window.location='http://localhost:8000/AAPL'
});

$("#li").click(function(event){
    console.log("this", this);
});