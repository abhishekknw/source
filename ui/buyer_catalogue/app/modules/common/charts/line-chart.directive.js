var app = angular.module('machadaloCommon');
  app.directive('lineChart',function() {
    return {
      restrict: 'E',
      scope: {
        // Bind the data to the directive scope.
        data: '=',
        // Allow the user to change the dimensions of the chart.
        height: '@',
        width: '@'
      },
      // The svg element is needed by D3.
      template: '<svg ng-attr-height="{{ height }}" ng-attr-width="{{ width }}"></svg>',
      link: function(scope, element) {
        var svg = element.find('svg'),
          chart;
          // alert("line");

        // This function is called when the data is changed.
        var update = function() {
          d3.select(svg[0])
            .datum(scope.data)
            .call(chart);
        };

        // Render the chart every time the data changes.
        // The data is serialized in order to easily check for changes.
        scope.$watch(function() { return angular.toJson(scope.data); }, function() {
          // The chart may not have been initialized at this point so we need
          // to account for that.
          if (chart) {
            update();
          }
        });

        // The chart can not be rendered at once, since the chart
        // creation is asynchronous.
        scope.$on('chartinit', update);

        nv.addGraph(function() {
          // This code is the same as the example before.
          chart = nv.models.lineChart()
            .showLegend(false)
            .showYAxis(true)
            .showXAxis(true);

          chart.xAxis
            .axisLabel('x')
            .tickFormat(d3.format('.2f'));

          chart.yAxis
            .axisLabel('y')
            .tickFormat(d3.format('.2f'));

          nv.utils.windowResize(function() {
            chart.update()
          });

          // Emit an event so we can know that the
          // chart has been initialized.
          scope.$emit('chartinit');

          return chart;
        });
      }
    }
  });
