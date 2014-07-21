(function() {
    var app;

    app = angular.module("ngQuickDate", []);

    app.directive("quickDatepicker", [
         '$filter', '$sce', function(ngQuickDateDefaults, $filter, $sce) {
            return {
                restrict: "E",
                replace: true,
                link: function(scope, element, attrs, ngModelCtrl) {
                    console.log('link');
                    return scope.weeks = [{day:0},{day:1},{day:2}]
                },
                templateUrl: "./tpl.html"
            };
        }
    ]);


}).call(this);

