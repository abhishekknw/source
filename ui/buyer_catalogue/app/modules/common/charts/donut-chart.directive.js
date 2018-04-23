var app = angular.module('machadaloCommon');

app.directive('donut', function() {
  return {
        restrict: 'E',
        scope: {
          // Bind the data to the directive scope.
          data: '=',
        },
           link: function(scope, element) {
                   //custom colors
                  //  alert("hello");
                  var color = d3.scale.ordinal()
                  .range(["#3399FF", "#5DAEF8", "#86C3FA", "#ADD6FB", "#D6EBFD"]);
                  console.log(scope.data);
                   var data = scope.data;
                   var width = 300;
                   var height = 300;
                   var pie = d3.layout.pie().sort(null);
                   var arc = d3.svg.arc()
                     .outerRadius(width / 2 * 0.9)
                     .innerRadius(width / 2 * 0.5)
                   var svg = d3.select(element[0]).append('svg')
                     .attr({width: width, height: height})
                     .append('g')
                     .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');
                     // add the <path>s for each arc slice
                  svg.selectAll('path').data(pie(data))
                     .enter().append('path')
                     .style('stroke', 'white')
                     .attr('d', arc)
                     .attr('fill', function(d, i){ return color(i) });
            }
   }

});
