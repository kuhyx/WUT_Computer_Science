import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface Zamowienie {
  id?: number;
  status: string;
}


@Component({
  selector: 'app-zamowienie',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './zamowienie.component.html',
  styleUrl: './zamowienie.component.css',
})
export class ZamowienieComponent {
  zamowienia: Zamowienie[] = [];
  newZamowienie: Zamowienie = { status: '' };
  editZamowienie: Zamowienie | null = null;
  private apiUrl = 'http://localhost:3000/api/zamowienie';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadZamowienia();
  }

  loadZamowienia(): void {
    this.http.get<Zamowienie[]>(this.apiUrl).subscribe(data => {
      this.zamowienia = data;
    });
  }

  createZamowienie(): void {
    this.http.post<Zamowienie>(this.apiUrl, this.newZamowienie).subscribe(data => {
      this.zamowienia.push(data);
      this.newZamowienie = { status: '' };
    });
  }

  updateZamowienie(): void {
    if (this.editZamowienie && this.editZamowienie.id) {
      this.http.put<Zamowienie>(`${this.apiUrl}/${this.editZamowienie.id}`, this.editZamowienie).subscribe(data => {
        this.loadZamowienia();
        this.editZamowienie = null;
      });
    }
  }

  deleteZamowienie(id: number): void {
    this.http.delete<Zamowienie>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.zamowienia = this.zamowienia.filter(z => z.id !== id);
    });
  }

  startEdit(zamowienie: Zamowienie): void {
    this.editZamowienie = { ...zamowienie };
  }

  cancelEdit(): void {
    this.editZamowienie = null;
  }
}
