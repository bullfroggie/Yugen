(function(angular) {
    let app = angular.module("app");

    app.controller("AddAccommodationCtrl", [
        "$http",
        "$state",
        "$stateParams",
        "$scope",
        "$timeout",
        "Upload",
        function($http, $state, $stateParams, $scope, $timeout, Upload) {
            let that = this;

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
                images: []
            };

            /*
            Image Upload
            */
            // $scope.uploadFiles = function(files) {
            //     $scope.files = files;
            //     if (files && files.length) {
            //         Upload.upload({
            //             url: "",
            //             data: {
            //                 files: files
            //             }
            //         }).then(
            //             function(response) {
            //                 $timeout(function() {
            //                     $scope.result = response.data;
            //                 });
            //             },
            //             function(response) {
            //                 if (response.status > 0) {
            //                     $scope.errorMsg = response.status + ": " + response.data;
            //                 }
            //             },
            //             function(evt) {
            //                 $scope.progress = Math.min(
            //                     100,
            //                     parseInt((100.0 * evt.loaded) / evt.total)
            //                 );
            //             }
            //         );
            //     }
            // };

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
                        $state.go("dashboard.admin_home");
                    },
                    function(reason) {
                        console.log(reason);
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
                    if ($scope.form.file.$valid && $scope.file) {
                        $scope.upload($scope.file);
                    }
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
