import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


interface ZamowioneDanie {
  id?: number;
  zamowienieId: number;
}

@Component({
  selector: 'app-zamowione-danie',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './zamowione-danie.component.html',
  styleUrl: './zamowione-danie.component.css',
})
export class ZamowioneDanieComponent {
  zamowioneDania: ZamowioneDanie[] = [];
  newZamowioneDanie: ZamowioneDanie = { zamowienieId: 0 };
  editZamowioneDanie: ZamowioneDanie | null = null;
  private apiUrl = 'http://localhost:3000/api/zamowione-danie';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadZamowioneDania();
  }

  loadZamowioneDania(): void {
    this.http.get<ZamowioneDanie[]>(this.apiUrl).subscribe(data => {
      this.zamowioneDania = data;
    });
  }

  createZamowioneDanie(): void {
    this.http.post<ZamowioneDanie>(this.apiUrl, this.newZamowioneDanie).subscribe(data => {
      this.zamowioneDania.push(data);
      this.newZamowioneDanie = { zamowienieId: 0 };
    });
  }

  updateZamowioneDanie(): void {
    if (this.editZamowioneDanie && this.editZamowioneDanie.id) {
      this.http.put<ZamowioneDanie>(`${this.apiUrl}/${this.editZamowioneDanie.id}`, this.editZamowioneDanie).subscribe(data => {
        this.loadZamowioneDania();
        this.editZamowioneDanie = null;
      });
    }
  }

  deleteZamowioneDanie(id: number): void {
    this.http.delete<ZamowioneDanie>(`${this.apiUrl}/${id}`).subscribe(() => {
      this.zamowioneDania = this.zamowioneDania.filter(z => z.id !== id);
    });
  }

  startEdit(zamowioneDanie: ZamowioneDanie): void {
    this.editZamowioneDanie = { ...zamowioneDanie };
  }

  cancelEdit(): void {
    this.editZamowioneDanie = null;
  }
}
