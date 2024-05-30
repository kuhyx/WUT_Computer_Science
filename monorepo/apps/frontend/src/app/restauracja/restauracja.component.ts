import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

interface Restauracja {
  id?: number;
  adres: string;
}

@Component({
  selector: 'app-restauracja',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './restauracja.component.html',
  styleUrl: './restauracja.component.css',
})
export class RestauracjaComponent {
  restauracje: Restauracja[] = [];
  newRestauracja: Restauracja = { adres: '' };
  editRestauracja: Restauracja | null = null;
  private apiUrl = 'http://localhost:3000/api/restauracja';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadRestauracje();
  }

  loadRestauracje(): void {
    this.http.get<Restauracja[]>(this.apiUrl).subscribe(data => {
      this.restauracje = data;
    });
  }

  createRestauracja(): void {
    this.http.post<Restauracja>(this.apiUrl, this.newRestauracja).subscribe(data => {
      this.restauracje.push(data);
      this.newRestauracja = { adres: '' };
    });
  }

  updateRestauracja(): void {
    if (this.editRestauracja && this.editRestauracja.id) {
      this.http.put<Restauracja>(`${this.apiUrl}/${this.editRestauracja.id}`, this.editRestauracja).subscribe(data => {
        this.loadRestauracje();
        this.editRestauracja = null;
      });
    }
  }

  deleteRestauracja(id: number): void {
    this.http.delete<Restauracja>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.restauracje = this.restauracje.filter(r => r.id !== id);
    });
  }

  startEdit(restauracja: Restauracja): void {
    this.editRestauracja = { ...restauracja };
  }

  cancelEdit(): void {
    this.editRestauracja = null;
  }
}
