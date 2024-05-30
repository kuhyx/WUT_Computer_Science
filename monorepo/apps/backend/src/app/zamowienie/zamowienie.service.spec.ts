import { Test, TestingModule } from '@nestjs/testing';
import { ZamowienieService } from './zamowienie.service';

describe('ZamowienieService', () => {
  let service: ZamowienieService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ZamowienieService],
    }).compile();

    service = module.get<ZamowienieService>(ZamowienieService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
