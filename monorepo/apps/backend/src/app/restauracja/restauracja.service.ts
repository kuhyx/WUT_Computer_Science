// src/restauracja/restauracja.service.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { Restauracja } from '@prisma/client';

@Injectable()
export class RestauracjaService {
  constructor(private prisma: DatabaseService) {}

  async findAll(): Promise<Restauracja[]> {
    return this.prisma.restauracja.findMany();
  }

  async findOne(id: number): Promise<Restauracja | null> {
    return this.prisma.restauracja.findUnique({ where: { id } });
  }

  async create(data: { adres: string }): Promise<Restauracja> {
    return this.prisma.restauracja.create({ data });
  }

  async update(id: number, data: Partial<Restauracja>): Promise<Restauracja> {
    return this.prisma.restauracja.update({ where: { id }, data });
  }

  async delete(id: number): Promise<Restauracja> {
    return this.prisma.restauracja.delete({ where: { id } });
  }
}
