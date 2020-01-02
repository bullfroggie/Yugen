(function(angular) {
    let app = angular.module("app", ["ui.router", "ui.bootstrap"]);

    app.config(["$stateProvider", "$urlRouterProvider", function($stateProvider, $urlRouterProvider) {
        $stateProvider
        .state("register", {
            url: "/register",
            templateUrl: "app/components/auth/register.tpl.html",
            controller: "AuthCtrl",
            controllerAs: "auth"
        })
        .state("login", {
            url: "/login",
            templateUrl: "app/components/auth/login.tpl.html",
            controller: "AuthCtrl",
            controllerAs: "auth"
        });

        $urlRouterProvider.otherwise("/register");
    }]);

})(angular);