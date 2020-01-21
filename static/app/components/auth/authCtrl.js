(function(angular) {
    let app = angular.module("app");

    app.controller("AuthCtrl", [
        "$scope",
        "$state",
        "$http",
        "$cookies",
        function($scope, $state, $http, $cookies) {
            let that = this;

            if ($cookies.get("yugen_user")) {
                $state.go("user_homepage");
            }

            $scope.alerts = [];

            $scope.addAlert = function(message) {
                $scope.alerts.push(message);
            };

            $scope.closeAlert = function(index) {
                $scope.alerts.splice(index, 1);
            };

            this.parseJwt = function(token) {
                var base64Url = token.split(".")[1];
                var base64 = base64Url.replace("-", "+").replace("_", "/");
                return JSON.parse($window.atob(base64));
            };

            this.newUser = {
                user_type: 2,
                first_name: "",
                last_name: "",
                username: "",
                password: "",
                date_of_birth: "",
                email: "",
                profile_image: "styles/images/regular_user_icon.png", // default profile image
                active: 1
            };

            this.login = {
                email: "",
                password: ""
            };

            /*
            Restrict registration to >= 18y/o
            */
            let tempDt = new Date();
            tempDt.setFullYear(tempDt.getFullYear() - 18);
            this.maxDt = tempDt.toISOString().slice(0, 10);

            this.registerUser = function() {
                $http.post("api/user/registration", that.newUser).then(
                    function(response) {
                        console.log(response);
                        if (response.status == 200) {
                            $state.go("login");
                        }
                    },
                    function(reason) {
                        console.log(reason);
                        if (reason.status == 409) {
                            $scope.addAlert({
                                type: "danger",
                                msg: reason.data
                            });
                        }
                    }
                );
            };

            this.userLogin = function() {
                $http.post("api/user/login", that.login).then(
                    function(response) {
                        console.log(response);
                        $state.go("user_homepage");
                    },
                    function(reason) {
                        console.log(reason);
                        if (reason.status == 401) {
                            $scope.addAlert({
                                type: "danger",
                                msg: reason.data
                            });
                        } else if (reason.status == 404) {
                            $scope.addAlert({
                                type: "danger",
                                msg: reason.data
                            });
                        }
                    }
                );
            };
        }
    ]);
})(angular);
