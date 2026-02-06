// src/app/uzytkownik/uzytkownik.component.ts
import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface Uzytkownik {
  id?: number;
  imie: string;
  nazwisko: string;
  adres: string;
  Historia_zamowienId: number;
}

@Component({
  selector: 'app-uzytkownik',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './uzytkownik.component.html',
  styleUrl: './uzytkownik.component.css',
})
export class UzytkownikComponent {
  uzytkownicy: Uzytkownik[] = [];
  newUzytkownik: Uzytkownik = { imie: '', nazwisko: '', adres: '', Historia_zamowienId: 0 };
  editUzytkownik: Uzytkownik | null = null;
  private apiUrl = 'http://localhost:3000/api/uzytkownik';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadUzytkownicy();
  }

  loadUzytkownicy(): void {
    this.http.get<Uzytkownik[]>(this.apiUrl).subscribe(data => {
      this.uzytkownicy = data;
    });
  }

  createUzytkownik(): void {
    this.http.post<Uzytkownik>(this.apiUrl, this.newUzytkownik).subscribe(data => {
      this.uzytkownicy.push(data);
      this.newUzytkownik = { imie: '', nazwisko: '', adres: '', Historia_zamowienId: 0 };
    });
  }

  updateUzytkownik(): void {
    if (this.editUzytkownik && this.editUzytkownik.id) {
      this.http.put<Uzytkownik>(`${this.apiUrl}/${this.editUzytkownik.id}`, this.editUzytkownik).subscribe(data => {
        this.loadUzytkownicy();
        this.editUzytkownik = null;
      });
    }
  }

  deleteUzytkownik(id: number): void {
    this.http.delete<Uzytkownik>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.uzytkownicy = this.uzytkownicy.filter(u => u.id !== id);
    });
  }

  startEdit(uzytkownik: Uzytkownik): void {
    this.editUzytkownik = { ...uzytkownik };
  }

  cancelEdit(): void {
    this.editUzytkownik = null;
  }
}
