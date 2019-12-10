(function(angular) {
    let app = angular.module("app", ["ui.router"]);

    app.config(["$stateProvider", "$urlRouterProvider", function($stateProvider, $urlRouterProvider) {
        $stateProvider
        .state("home", {
            url: "/",
            templateUrl: "app/components/users/users.tpl.html",
            controller: "UsersCtrl",
            controllerAs: "usrctrl"
        });

        $urlRouterProvider.otherwise("/");
    }]);

})(angular);