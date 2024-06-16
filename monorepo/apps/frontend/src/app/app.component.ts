import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatCardModule} from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button'
import {MatTabsModule} from '@angular/material/tabs';
import {MatMenuModule} from '@angular/material/menu';
import { MatToolbarModule } from '@angular/material/toolbar'
import { MatIconModule } from '@angular/material/icon'



@Component({
  standalone: true,
  imports: [RouterModule, MatGridListModule, MatCardModule, MatButtonModule, MatTabsModule, MatMenuModule, MatToolbarModule,
    MatIconModule
  ],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'frontend';

  menuItems = [
    { title: 'Danie', path: '/danie', icon: 'restaurant' },
    { title: 'Historia Zamówien', path: '/historia-zamowien', icon: 'history' },
    { title: 'Recenzja', path: '/recenzja', icon: 'rate_review' },
    { title: 'Restauracja', path: '/restauracja', icon: 'store' },
    { title: 'Użytkownik', path: '/uzytkownik', icon: 'person' },
    { title: 'Zamówienie', path: '/zamowienie', icon: 'receipt' },
    { title: 'Zamówione Danie', path: '/zamowione-danie', icon: 'local_dining' },
    { title: 'Zniżka', path: '/znizka', icon: 'local_offer' }
  ];

  activeLink = this.menuItems[0].path;

}
