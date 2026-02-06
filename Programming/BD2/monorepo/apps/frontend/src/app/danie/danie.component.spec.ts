import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DanieComponent } from './danie.component';

describe('DanieComponent', () => {
  let component: DanieComponent;
  let fixture: ComponentFixture<DanieComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DanieComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DanieComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
