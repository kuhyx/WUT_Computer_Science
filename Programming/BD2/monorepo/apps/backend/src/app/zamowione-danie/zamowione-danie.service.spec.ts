import { Test, TestingModule } from '@nestjs/testing';
import { ZamowioneDanieService } from './zamowione-danie.service';

describe('ZamowioneDanieService', () => {
  let service: ZamowioneDanieService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ZamowioneDanieService],
    }).compile();

    service = module.get<ZamowioneDanieService>(ZamowioneDanieService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
