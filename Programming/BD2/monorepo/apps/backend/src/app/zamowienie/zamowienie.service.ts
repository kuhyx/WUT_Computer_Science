// src/zamowienie/zamowienie.service.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { Zamowienie } from '@prisma/client';

@Injectable()
export class ZamowienieService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Zamowienie[]> {
    return this.prisma.zamowienie.findMany();
  }

  async findOne(id: number): Promise<Zamowienie | null> {
    return this.prisma.zamowienie.findUnique({ where: { id } });
  }

  async create(data: { status: string }): Promise<Zamowienie> {
    return this.prisma.zamowienie.create({ data });
  }

  async update(id: number, data: Partial<Zamowienie>): Promise<Zamowienie> {
    return this.prisma.zamowienie.update({ where: { id }, data });
  }

  async delete(id: number): Promise<Zamowienie> {
    return this.prisma.zamowienie.delete({ where: { id } });
  }
}
