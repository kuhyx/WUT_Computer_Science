workspace "Name" "Description" {

    !identifiers hierarchical

    model {
        admin = person "Administrator" "Administrator zarządzający systemem e-Toll"
        kierowca = person "Kierowca" "Kierowca korzystający z płatnych dróg w systemie e-Toll"
        archiwum = softwareSystem "System agregacji danych historycznych" "Archiwum danych do celów statystycznych"
        systemPlatnosci = softwareSystem "System procesowania płatności" "System odpowiedzialny za obsługę płatności dokonywanych prze użytkowników"

        systemEtoll = softwareSystem "System e-Toll" {
            webApp = container "Aplikacja webowa" "Służy do zarządzania kontem oraz systemem"
            mobileApp = container "Aplikacja mobilna" "Pozwala na śledzenie pozycji pojazdu w celu dokonywania opłat"
            embeddedApp = container "Aplikacja na dedykowane urządzenia zbierania opłat" "Działa na dedykowanych urządzeniach śledzących pozycję pojazdu"

            serverApp = container "Aplikacja serwerowa" "Obsługuje logikę działania systemu" {
                mainComponent = component "MainComponent" "Centralny element aplikacji odpowiedzialny za jej działanie" 
                signinController = component "SigninController" "Odpowiada za logowanie do systemu i autoryzację"
                tollController = component "TollController" "Odpowiada za kontrolowanie wysokości opłat"

                userService = component "UserService" "Zawiera logikę biznesową dotyczącą użytkowników"
                paymentService = component "PaymentService" "Zawiera logikę dotyczącą przetwarzania płatności"
                userRepository = component "UserRepository" "Odpowiada za dostęp do danych użytkownika"
                paymentRepository = component "PaymentRepository" "Odpowiada za dostęp do danych płatności"

                positionService = component "PositionService" "Odpowiada za określanie pozycji pojazdu w kontekście odcinków dróg"

                mainComponent -> signinController "Używa"
                mainComponent -> tollController "Używa"
                signinController -> userService "Używa"
                mainComponent -> paymentService "Używa"
                tollController -> positionService "Używa"

                userService -> userRepository "Odczytuje/zapisuje dane"
                paymentService -> paymentRepository "Odczytuje/zapisuje dane"
            }

            db = container "Baza danych" {
                tags "Database"
            }

            serverApp -> db "Czyta i zapisuje dane"
            webApp -> serverApp
            mobileApp -> serverApp
            embeddedApp -> serverApp
        }

        admin -> systemEtoll.webApp "Zarządza systemem"
        kierowca -> systemEtoll "Korzysta z systemu"

        kierowca -> systemEtoll.webApp "Zarządza kontem"
        kierowca -> systemEtoll.mobileApp "Opłaca przejazdy"
        kierowca -> systemEtoll.embeddedApp "Opłaca przejazdy"

        systemEtoll.serverApp -> systemPlatnosci "Realizuje płatność"
        systemEtoll.serverApp -> archiwum "Przekazuje dane o użyciu dróg"

        liveDeployment = deploymentEnvironment "Deployment" {
            deploymentNode "Urządzenie mobilne klienta" "" "Apple iOS or Android" {
                liveMobileAppInstance = containerInstance systemEtoll.mobileApp
            }

            deploymentNode "Dedykowane urządzenie zbierania opłat" "" "Linux" {
                liveEmbeddedAppInstance = containerInstance systemEtoll.embeddedApp
            }

            deploymentNode "Urządzenie klienta" "" "Laptop/Desktop" {
                deploymentNode "Przeglądarka internetowa" "" "Chromium/Firefox" {
                    browserInstance = containerInstance systemEtoll.webApp
                }
            }

            deploymentNode "System e-Toll" "" "Data Center dla systemu e-Toll" {
                deploymentNode "etoll-server" "" "Ubuntu Server 24.04 LTS" "" 4 {
                    deploymentNode "Apache Tomcat" "" "Apache Tomcat 8.x" {
                        liveWebApplicationInstance = containerInstance systemEtoll.serverApp
                    }
                }

                db1 = deploymentNode "etoll-db01" "" "Ubuntu Server 24.04 LTS" {
                    primaryDatabaseServer = deploymentNode "Oracle - Primary" "" "Oracle 12c" {
                        livePrimaryDatabaseInstance = containerInstance systemEtoll.db
                    }
                }
                db2 = deploymentNode "etoll-db02" "" "Ubuntu Server 24.04 LTS" "Failover" {
                    secondaryDatabaseServer = deploymentNode "Oracle - Secondary" "" "Oracle 12c" "Failover" {
                        liveSecondaryDatabaseInstance = containerInstance systemEtoll.db "Failover"
                    }
                }
                deploymentNode "etoll-prod001" "" "" "" {
                    softwareSystemInstance systemEtoll
                }

                db1.primaryDatabaseServer -> db2.secondaryDatabaseServer "Replikuje dane"
            }
        }
    }

    views {
        systemContext systemEtoll "SystemContext" {
            include *
            autolayout bt
        }

        container systemEtoll "Container" {
            include *
        }

        # component systemEtoll.webApp "ComponentWebApp" {
        #     include *
        # }

        # component systemEtoll.mobileApp "ComponentMobileApp" {
        #     include *
        # }

        # component systemEtoll.embeddedApp "ComponentEmbeddedApp" {
        #     include *
        # }

        component systemEtoll.serverApp "ComponentServerApp" {
            include *
            autoLayout bt
        }

        deployment systemEtoll "Deployment" {
            include *
            autoLayout lr
        }

        styles {
            element "Element" {
                color #ffffff
            }
            element "Person" {
                background #199b65
                shape person
            }
            element "Software System" {
                background #1eba79
            }
            element "Container" {
                background #23d98d
            }
            element "Database" {
                shape cylinder
            }
        }
    }

    configuration {
        scope softwaresystem
    }

}