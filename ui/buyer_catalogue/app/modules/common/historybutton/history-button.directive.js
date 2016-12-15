angular.module("machadaloCommon")
.directive("backButton", ["$window", function ($window) {
    return {
        restrict: "E",
        templateUrl: 'modules/common/historybutton/history-button.tmpl.html',
        link: function (scope, elem, attrs) {
            elem.bind("click", function () {
                $window.history.back();
            });
        }
    };
}]);
