(function(angular) {
    let app = angular.module("app");

    app.controller("AddAccommodationCtrl", [
        "$http",
        "$state",
        "$stateParams",
        "$scope",
        "Upload",
        function($http, $state, $stateParams, $scope, Upload) {
            let that = this;

            $scope.alerts = [];

            $scope.addAlert = function(message) {
                $scope.alerts.push(message);
            };

            $scope.closeAlert = function(index) {
                $scope.alerts.splice(index, 1);
            };

            this.cities = [];
            this.accommodationTypes = [];

            this.editCheck = false;

            this.newAccommodation = {
                accommodation_types_id: 1,
                cities_id: 1688169087,
                name: "",
                price_per_night: 0.0,
                stars: 1,
                street_address: "",
                description: "",
                breakfast: 0,
                internet: 0,
                available: 0
            };

            this.images = null;

            /*
            Image Upload
            */
            this.uploadPic = function(file) {
                if (file) {
                    try {
                        Upload.upload({
                            url: "api/accommodation/upload/" + that.newAccommodation.name,
                            method: "POST",
                            data: { file: file }
                        })
                            .then(function onSuccess(response) {
                                console.log("Upload successful.", response);
                            })
                            .catch(function onError(response) {
                                console.log("Upload failed.", response);
                            });
                    } catch (error) {
                        console.log(error.message);
                    }
                }
            };

            this.getCities = function() {
                $http.get("/api/cities").then(
                    function(response) {
                        console.log(response);
                        that.cities = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAccommodationTypes = function() {
                $http.get("/api/accommodation/types").then(
                    function(response) {
                        console.log(response);
                        that.accommodationTypes = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.addAccommodation = function() {
                $http.post("/api/accommodation", that.newAccommodation).then(
                    function(response) {
                        console.log(response);
                        that.uploadPic(that.images);
                        $state.go("dashboard.admin_home");
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

            this.getAccommodation = function(id) {
                $http.get("api/accommodation/" + id).then(
                    function(response) {
                        console.log(response);
                        that.newAccommodation = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.editAccommodation = function(id) {
                $http.put("api/accommodation/edit/" + id, that.newAccommodation).then(
                    function(response) {
                        console.log(response);
                        $state.go("dashboard.admin_home");
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.save = function() {
                if ($stateParams["id"]) {
                    that.editAccommodation($stateParams["id"]);
                } else {
                    that.addAccommodation();
                }
            };

            if ($stateParams["id"]) {
                that.getAccommodation($stateParams["id"]);
                that.editCheck = true;
            }

            this.getCities();
            this.getAccommodationTypes();
        }
    ]);
})(angular);
