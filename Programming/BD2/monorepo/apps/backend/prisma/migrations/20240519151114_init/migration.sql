/*
  Warnings:

  - A unique constraint covering the columns `[zamowienieId]` on the table `Zamowione_danie` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `zamowienieId` to the `Zamowione_danie` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Zamowione_danie" ADD COLUMN     "zamowienieId" INTEGER NOT NULL;

-- CreateTable
CREATE TABLE "_DanieZamowione_danie" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "_DanieZamowione_danie_AB_unique" ON "_DanieZamowione_danie"("A", "B");

-- CreateIndex
CREATE INDEX "_DanieZamowione_danie_B_index" ON "_DanieZamowione_danie"("B");

-- CreateIndex
CREATE UNIQUE INDEX "Zamowione_danie_zamowienieId_key" ON "Zamowione_danie"("zamowienieId");

-- AddForeignKey
ALTER TABLE "Zamowione_danie" ADD CONSTRAINT "Zamowione_danie_zamowienieId_fkey" FOREIGN KEY ("zamowienieId") REFERENCES "Zamowienie"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_DanieZamowione_danie" ADD CONSTRAINT "_DanieZamowione_danie_A_fkey" FOREIGN KEY ("A") REFERENCES "Danie"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_DanieZamowione_danie" ADD CONSTRAINT "_DanieZamowione_danie_B_fkey" FOREIGN KEY ("B") REFERENCES "Zamowione_danie"("id") ON DELETE CASCADE ON UPDATE CASCADE;
