(function(angular) {
    let app = angular.module("app");

    app.controller("UserCtrl", [
        "$http",
        "$state",
        function($http, $state) {
            let that = this;

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
                        $state.go("register");
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
