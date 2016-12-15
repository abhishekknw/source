angular.module('machadaloCommon')
    .directive('ngLoading', ["$compile", function ($compile) {

    var loadingSpinner = '<div class="spinner">  <div class="bounce1"></div>  <div class="bounce2"></div>  <div class="bounce3"></div></div>';
    console.log(loadingSpinner);
    // alert("hi");
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var originalContent = element.html();
            element.html(loadingSpinner);
            scope.$watch(attrs.ngLoading, function (val) {
                if(val) {
                    element.html(originalContent);
                    $compile(element.contents())(scope);
                } else {
                    element.html(loadingSpinner);
                }
            });
        }
    };
}]);
