(function(angular) {
    let app = angular.module("app", ["ui.router", "ui.bootstrap", "ngCookies"]);

    app.config([
        "$stateProvider",
        "$urlRouterProvider",
        function($stateProvider, $urlRouterProvider) {
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
                })
                .state("user_homepage", {
                    url: "/",
                    templateUrl: "app/components/nav/dashboard.tpl.html",
                    controller: "UserCtrl",
                    controllerAs: "uctrl"
                })
                .state("admin_homepage", {
                    url: "/admin",
                    templateUrl: "app/components/nav/dashboard.tpl.html",
                    controller: "AdminCtrl",
                    controllerAs: "actrl"
                });

            $urlRouterProvider.otherwise("/register");
        }
    ]);
})(angular);
