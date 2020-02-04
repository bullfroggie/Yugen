(function(angular) {
    let app = angular.module("app", ["ui.router", "ui.bootstrap", "ngCookies", "ngFileUpload"]);

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
                .state("dashboard", {
                    url: "/dashboard",
                    templateUrl: "app/components/nav/dashboard.tpl.html",
                    controller: "DashboardCtrl",
                    controllerAs: "dctrl"
                })
                .state("dashboard.admin_home", {
                    url: "/home",
                    templateUrl: "app/components/admin/homepage/adminHome.tpl.html",
                    controller: "AdminHomeCtrl",
                    controllerAs: "ahctrl"
                })
                .state("dashboard.add_admin", {
                    url: "/add_admin",
                    templateUrl: "app/components/admin/add_admin/adminForm.tpl.html",
                    controller: "AddAdminCtrl",
                    controllerAs: "aactrl"
                })
                .state("dashboard.add_accommodation", {
                    url: "/add_accommodation",
                    templateUrl:
                        "app/components/admin/add_accommodation/accommodationForm.tpl.html",
                    controller: "AddAccommodationCtrl",
                    controllerAs: "aactrl"
                })
                .state("dashboard.edit_accommodation", {
                    url: "/add_accommodation/{id}",
                    templateUrl:
                        "app/components/admin/add_accommodation/accommodationForm.tpl.html",
                    controller: "AddAccommodationCtrl",
                    controllerAs: "aactrl"
                })
                .state("dashboard.add_flight", {
                    url: "/add_flight",
                    templateUrl: "app/components/admin/add_flight/flightForm.tpl.html",
                    controller: "AddFlightCtrl",
                    controllerAs: "afctrl"
                })
                .state("dashboard.edit_flight", {
                    url: "/add_flight/{id}",
                    templateUrl: "app/components/admin/add_flight/flightForm.tpl.html",
                    controller: "AddFlightCtrl",
                    controllerAs: "afctrl"
                })
                .state("dashboard.user_home", {
                    url: "/",
                    templateUrl: "app/components/regular_user/homepage/homepage.tpl.html",
                    controller: "UserHomeCtrl",
                    controllerAs: "uhctrl"
                })
                .state("dashboard.accommodation", {
                    url: "/accommodation",
                    templateUrl:
                        "app/components/regular_user/accommodation/accommodation_home.tpl.html",
                    controller: "AccommodationCtrl",
                    controllerAs: "acctrl"
                })
                .state("dashboard.details", {
                    url: "/details/{id}",
                    templateUrl:
                        "app/components/regular_user/accommodation/accommodation_details/accommodation_details.tpl.html",
                    controller: "DetailsCtrl",
                    controllerAs: "dctrl"
                })
                .state("dashboard.flights", {
                    url: "/flights",
                    templateUrl: "app/components/regular_user/flights/flights.tpl.html",
                    controller: "FlightsCtrl",
                    controllerAs: "fctrl"
                })
                .state("dashboard.reservations_and_tickets", {
                    url: "/reservations_and_tickets",
                    templateUrl:
                        "app/components/regular_user/reservations_and_tickets/reservations-and-tickets.tpl.html",
                    controller: "ReservationsAndTicketsCtrl",
                    controllerAs: "ratctrl"
                });

            $urlRouterProvider.otherwise("/dashboard");
        }
    ]);
})(angular);
