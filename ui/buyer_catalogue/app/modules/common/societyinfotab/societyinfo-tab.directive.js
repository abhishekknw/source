angular.module('machadaloCommon')
.directive('societyinfoTab', function() {
  return {
  restrict: 'E',
  templateUrl: 'modules/common/societyinfotab/societyinfo-tab.tmpl.html',
  link: function(scope, element, attrs) {

  }};
}).directive('showtab', function() {
  return {
  restrict: 'E',
  //templateUrl: 'modules/common/societyinfotab/societyinfo-tab.tmpl.html',
  link: function(scope, element, attrs) {
    alert('vidhi');
    element.click(function(e) {
                        e.preventDefault();
                        $(element).tab('show');
                    });
  }};
});
