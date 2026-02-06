// src/app/danie/danie.component.ts
import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Danie {
  id?: number;
  cena: number;
  kategoria: string;
  nazwa: string;
}

@Component({
  selector: 'app-danie',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './danie.component.html',
  styleUrl: './danie.component.css',
})
export class DanieComponent {
  dania: Danie[] = [];
  newDanie: Danie = { cena: 0, kategoria: '', nazwa: '' };
  editDanie: Danie | null = null;
  private apiUrl = 'http://localhost:3000/api/danie';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadDania();
  }

  loadDania(): void {
    this.http.get<Danie[]>(this.apiUrl).subscribe(data => {
      this.dania = data;
    });
  }

  createDanie(): void {
    this.http.post<Danie>(this.apiUrl, this.newDanie).subscribe(data => {
      this.dania.push(data);
      this.newDanie = { cena: 0, kategoria: '', nazwa: '' };
    });
  }

  updateDanie(): void {
    if (this.editDanie && this.editDanie.id) {
      this.http.put<Danie>(`${this.apiUrl}/${this.editDanie.id}`, this.editDanie).subscribe(data => {
        this.loadDania();
        this.editDanie = null;
      });
    }
  }

  deleteDanie(id: number): void {
    this.http.delete<Danie>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.dania = this.dania.filter(d => d.id !== id);
    });
  }

  startEdit(danie: Danie): void {
    this.editDanie = { ...danie };
  }

  cancelEdit(): void {
    this.editDanie = null;
  }
}
