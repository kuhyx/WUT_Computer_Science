import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

interface Znizka {
  id?: number;
  kod: string;
  wartosc: number;
  czy_dostepna: boolean;
  restauracjaId: number;
}


@Component({
  selector: 'app-znizka',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './znizka.component.html',
  styleUrl: './znizka.component.css',
})
export class ZnizkaComponent {
  znizki: Znizka[] = [];
  newZnizka: Znizka = { kod: '', wartosc: 0, czy_dostepna: true, restauracjaId: 0 };
  editZnizka: Znizka | null = null;
  private apiUrl = 'http://localhost:3000/api/znizka';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadZnizki();
  }

  loadZnizki(): void {
    this.http.get<Znizka[]>(this.apiUrl).subscribe(data => {
      this.znizki = data;
    });
  }

  createZnizka(): void {
    this.http.post<Znizka>(this.apiUrl, this.newZnizka).subscribe(data => {
      this.znizki.push(data);
      this.newZnizka = { kod: '', wartosc: 0, czy_dostepna: true, restauracjaId: 0 };
    });
  }

  updateZnizka(): void {
    if (this.editZnizka && this.editZnizka.id) {
      this.http.put<Znizka>(`${this.apiUrl}/${this.editZnizka.id}`, this.editZnizka).subscribe(data => {
        this.loadZnizki();
        this.editZnizka = null;
      });
    }
  }

  deleteZnizka(id: number): void {
    this.http.delete<Znizka>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.znizki = this.znizki.filter(z => z.id !== id);
    });
  }

  startEdit(znizka: Znizka): void {
    this.editZnizka = { ...znizka };
  }

  cancelEdit(): void {
    this.editZnizka = null;
  }
}
