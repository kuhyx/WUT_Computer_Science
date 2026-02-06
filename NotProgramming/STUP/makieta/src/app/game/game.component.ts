import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [        MatToolbarModule,
    MatCardModule,
    MatButtonModule, RouterModule],
  templateUrl: './game.component.html',
  styleUrl: './game.component.scss'
})
export class GameComponent {
  leftSide: string[] = ['wolf', 'goat', 'cabbage'];
  rightSide: string[] = [];
  boatOnLeft: boolean = true;

  move(what: string) {}
}
