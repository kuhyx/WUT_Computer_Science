// src/uzytkownik/uzytkownik.service.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { Uzytkownik } from '@prisma/client';

@Injectable()
export class UzytkownikService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Uzytkownik[]> {
    return this.prisma.uzytkownik.findMany();
  }

  async findOne(id: number): Promise<Uzytkownik | null> {
    return this.prisma.uzytkownik.findUnique({ where: { id } });
  }

  async create(data: { imie: string; nazwisko: string; adres: string; Historia_zamowienId: number }): Promise<Uzytkownik> {
    return this.prisma.uzytkownik.create({ data });
  }

  async update(id: number, data: Partial<Uzytkownik>): Promise<Uzytkownik> {
    return this.prisma.uzytkownik.update({ where: { id }, data });
  }

  async delete(id: number): Promise<Uzytkownik> {
    return this.prisma.uzytkownik.delete({ where: { id } });
  }
}
