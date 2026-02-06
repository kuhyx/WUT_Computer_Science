import { Route } from '@angular/router';
import { RestauracjaComponent } from './restauracja/restauracja.component';
import { RecenzjaComponent } from './recenzja/recenzja.component';
import { UzytkownikComponent } from './uzytkownik/uzytkownik.component';
import { ZamowienieComponent } from './zamowienie/zamowienie.component';
import { ZamowioneDanieComponent } from './zamowione-danie/zamowione-danie.component';
import { ZnizkaComponent } from './znizka/znizka.component';
import { HistoriaZamowienComponent } from './historia-zamowien/historia-zamowien.component';
import { DanieComponent } from './danie/danie.component';

export const appRoutes: Route[] = [
    {path: 'restauracja', component: RestauracjaComponent},
    {path: 'uzytkownik', component: UzytkownikComponent},
    {path: 'zamowienie', component: ZamowienieComponent},
    {path: 'zamowione-danie', component: ZamowioneDanieComponent},
    {path: 'znizka', component: ZnizkaComponent},
    {path: 'historia-zamowien', component: HistoriaZamowienComponent},
    {path: 'danie', component: DanieComponent},
    {path: 'recenzja', component: RecenzjaComponent}
];
