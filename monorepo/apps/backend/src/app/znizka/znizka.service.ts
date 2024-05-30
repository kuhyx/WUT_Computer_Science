// src/znizka/znizka.service.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { Znizka } from '@prisma/client';

@Injectable()
export class ZnizkaService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Znizka[]> {
    return this.prisma.znizka.findMany();
  }

  async findOne(id: number): Promise<Znizka | null> {
    return this.prisma.znizka.findUnique({ where: { id } });
  }

  async create(data: { kod: string; wartosc: number; czy_dostepna: boolean; restauracjaId: number }): Promise<Znizka> {
    return this.prisma.znizka.create({ data });
  }

  async update(id: number, data: Partial<Znizka>): Promise<Znizka> {
    return this.prisma.znizka.update({ where: { id }, data });
  }

  async delete(id: number): Promise<Znizka> {
    return this.prisma.znizka.delete({ where: { id } });
  }
}
