import { Routes } from '@angular/router';
import { IntroductionComponent } from './introduction/introduction.component';
import { GameComponent } from './game/game.component';
import { ReportComponent } from './report/report.component';

export const routes: Routes = [
  { path: '', redirectTo: '/introduction', pathMatch: 'full' },
  { path: 'introduction', component: IntroductionComponent },
  { path: 'game', component: GameComponent },
  { path: 'report', component: ReportComponent },
];