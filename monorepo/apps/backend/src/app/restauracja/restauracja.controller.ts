// src/restauracja/restauracja.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { RestauracjaService } from './restauracja.service';
import { Restauracja } from '@prisma/client';

@Controller('restauracja')
export class RestauracjaController {
  constructor(private readonly restauracjaService: RestauracjaService) {}

  @Get()
  async findAll(): Promise<Restauracja[]> {
    return this.restauracjaService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Restauracja | null> {
    return this.restauracjaService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { adres: string }): Promise<Restauracja> {
    return this.restauracjaService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Restauracja>): Promise<Restauracja> {
    return this.restauracjaService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Restauracja> {
    return this.restauracjaService.delete(+id);
  }
}
