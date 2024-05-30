import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HistoriaZamowienComponent } from './historia-zamowien.component';

describe('HistoriaZamowienComponent', () => {
  let component: HistoriaZamowienComponent;
  let fixture: ComponentFixture<HistoriaZamowienComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HistoriaZamowienComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HistoriaZamowienComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
