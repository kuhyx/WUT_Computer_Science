import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ZamowioneDanieComponent } from './zamowione-danie.component';

describe('ZamowioneDanieComponent', () => {
  let component: ZamowioneDanieComponent;
  let fixture: ComponentFixture<ZamowioneDanieComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ZamowioneDanieComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ZamowioneDanieComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
