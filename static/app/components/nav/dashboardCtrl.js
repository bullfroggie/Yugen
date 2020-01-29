(function(angular) {
    let app = angular.module("app");

    app.controller("DashboardCtrl", [
        "$http",
        "$state",
        "$cookies",
        function($http, $state, $cookies) {
            let that = this;

            if (!$cookies.get("yugen_user")) {
                $state.go("login");
            }

            this.loggedIn = {
                id: null,
                user_types_id: null,
                first_name: "",
                last_name: "",
                profile_image: ""
            };

            this.getUser = function() {
                $http.get("api/user").then(
                    function(response) {
                        console.log(response);
                        that.loggedIn = {
                            id: response.data.id,
                            user_types_id: response.data.user_types_id,
                            first_name: response.data.first_name,
                            last_name: response.data.last_name,
                            profile_image: response.data.profile_image
                        };

                        if (response.data.user_types_id == 1) {
                            $state.go("dashboard.admin_home");
                        } else if (response.data.user_types_id == 2) {
                            $state.go("dashboard.user_home");
                        }
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.userLogout = function() {
                $http.post("api/user/logout").then(
                    function(response) {
                        console.log(response);
                        $state.go("login");
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getUser();
        }
    ]);
})(angular);
