import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ZnizkaComponent } from './znizka.component';

describe('ZnizkaComponent', () => {
  let component: ZnizkaComponent;
  let fixture: ComponentFixture<ZnizkaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ZnizkaComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ZnizkaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
