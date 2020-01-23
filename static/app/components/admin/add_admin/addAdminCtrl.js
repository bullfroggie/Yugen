(function(angular) {
    let app = angular.module("app");

    app.controller("AddAdminCtrl", [
        "$http",
        "$state",
        "$scope",
        function($http, $state, $scope) {
            let that = this;

            $scope.alerts = [];

            $scope.addAlert = function(message) {
                $scope.alerts.push(message);
            };

            $scope.closeAlert = function(index) {
                $scope.alerts.splice(index, 1);
            };

            this.newAdmin = {
                user_type: 1,
                first_name: "",
                last_name: "",
                username: "",
                password: "",
                date_of_birth: "",
                email: "",
                profile_image: null,
                active: 1
            };

            /*
            Restrict registration to >= 18y/o
            */
            let tempDt = new Date();
            tempDt.setFullYear(tempDt.getFullYear() - 18);
            this.maxDt = tempDt.toISOString().slice(0, 10);

            this.addAdmin = function() {
                $http.post("api/user/registration", that.newAdmin).then(
                    function(response) {
                        console.log(response);
                        $scope.addAlert({
                            type: "success",
                            msg: "Successfully added a new Administrator!"
                        });
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
        }
    ]);
})(angular);
