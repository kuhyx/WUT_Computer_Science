import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Recenzja {
  id?: number;
  tekst: string;
  wartosc: number;
  restauracjaId: number;
  uzytkownikId: number;
}
@Component({
  selector: 'app-recenzja',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './recenzja.component.html',
  styleUrl: './recenzja.component.css',
})
export class RecenzjaComponent {
  recenzje: Recenzja[] = [];
  newRecenzja: Recenzja = { tekst: '', wartosc: 0, restauracjaId: 0, uzytkownikId: 0 };
  editRecenzja: Recenzja | null = null;
  private apiUrl = 'http://localhost:3000/api/recenzja';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadRecenzje();
  }

  loadRecenzje(): void {
    this.http.get<Recenzja[]>(this.apiUrl).subscribe(data => {
      this.recenzje = data;
    });
  }

  createRecenzja(): void {
    this.http.post<Recenzja>(this.apiUrl, this.newRecenzja).subscribe(data => {
      this.recenzje.push(data);
      this.newRecenzja = { tekst: '', wartosc: 0, restauracjaId: 0, uzytkownikId: 0 };
    });
  }

  updateRecenzja(): void {
    if (this.editRecenzja && this.editRecenzja.id) {
      this.http.put<Recenzja>(`${this.apiUrl}/${this.editRecenzja.id}`, this.editRecenzja).subscribe(data => {
        this.loadRecenzje();
        this.editRecenzja = null;
      });
    }
  }

  deleteRecenzja(id: number): void {
    this.http.delete<Recenzja>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.recenzje = this.recenzje.filter(r => r.id !== id);
    });
  }

  startEdit(recenzja: Recenzja): void {
    this.editRecenzja = { ...recenzja };
  }

  cancelEdit(): void {
    this.editRecenzja = null;
  }
}
