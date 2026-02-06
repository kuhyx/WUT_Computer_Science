import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RecenzjaComponent } from './recenzja.component';

describe('RecenzjaComponent', () => {
  let component: RecenzjaComponent;
  let fixture: ComponentFixture<RecenzjaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecenzjaComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(RecenzjaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
