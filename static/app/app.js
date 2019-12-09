(function(angular) {
    let app = angular.module("app", ["ui.router"]);

    app.config(["$stateProvider", "$urlRouterProvider", function($stateProvider, $urlRouterProvider) {
        $stateProvider
        .state("home", {
            url: "/"
        });

        $urlRouterProvider.otherwise("/");
    }]);

})(angular);