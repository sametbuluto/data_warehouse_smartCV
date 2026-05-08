import type { LucideIcon } from "lucide-react";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";

import { cn } from "../../lib/utils";
import { Card, CardContent } from "../ui/card";

interface KpiCardProps {
  title: string;
  value: string;
  subtitle: string;
  icon: LucideIcon;
  accentClassName?: string;
}

export function KpiCard({ title, value, subtitle, icon: Icon, accentClassName }: KpiCardProps) {
  return (
    <motion.div whileHover={{ y: -5 }} transition={{ duration: 0.18 }}>
      <Card className={cn("overflow-hidden", accentClassName)}>
        <CardContent className="relative p-6">
          <div className="absolute right-4 top-4 rounded-full bg-white/10 p-2 text-primary dark:bg-white/6">
            <ArrowUpRight className="h-4 w-4" />
          </div>

          <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-[20px] bg-primary/10 text-primary">
            <Icon className="h-5 w-5" />
          </div>

          <div className="space-y-1">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="text-3xl font-semibold tracking-tight text-foreground">{value}</p>
            <p className="text-xs leading-5 text-muted-foreground">{subtitle}</p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
