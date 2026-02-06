// src/app/historia-zamowien/historia-zamowien.component.ts
import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface HistoriaZamowien {
  id?: number;
  data_zamowienia: string;
}

@Component({
  selector: 'app-historia-zamowien',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './historia-zamowien.component.html',
  styleUrl: './historia-zamowien.component.css',
})
export class HistoriaZamowienComponent {
  historiaZamowien: HistoriaZamowien[] = [];
  newHistoriaZamowien: HistoriaZamowien = { data_zamowienia: '' };
  editHistoriaZamowien: HistoriaZamowien | null = null;
  private apiUrl = 'http://localhost:3000/api/historia-zamowien';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadHistoriaZamowien();
  }

  loadHistoriaZamowien(): void {
    this.http.get<HistoriaZamowien[]>(this.apiUrl).subscribe(data => {
      this.historiaZamowien = data;
    });
  }

  createHistoriaZamowien(): void {
    this.http.post<HistoriaZamowien>(this.apiUrl, this.newHistoriaZamowien).subscribe(data => {
      this.historiaZamowien.push(data);
      this.newHistoriaZamowien = { data_zamowienia: '' };
    });
  }

  updateHistoriaZamowien(): void {
    if (this.editHistoriaZamowien && this.editHistoriaZamowien.id) {
      this.http.put<HistoriaZamowien>(`${this.apiUrl}/${this.editHistoriaZamowien.id}`, this.editHistoriaZamowien).subscribe(data => {
        this.loadHistoriaZamowien();
        this.editHistoriaZamowien = null;
      });
    }
  }

  deleteHistoriaZamowien(id: number): void {
    this.http.delete<HistoriaZamowien>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.historiaZamowien = this.historiaZamowien.filter(h => h.id !== id);
    });
  }

  startEdit(historia: HistoriaZamowien): void {
    this.editHistoriaZamowien = { ...historia };
  }

  cancelEdit(): void {
    this.editHistoriaZamowien = null;
  }
}

